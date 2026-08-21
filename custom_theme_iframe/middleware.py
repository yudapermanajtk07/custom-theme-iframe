class ForceLightModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/xblock/') and 'text/html' in response.get('Content-Type', ''):
            try:
                content = response.content.decode('utf-8')
                
                # Inject Script and CSS to force light mode logically and visually
                injection = \"\"\"
                <script>
                  // Force theme to light immediately
                  document.documentElement.setAttribute('data-theme', 'light');
                  
                  // Set up an observer to stubbornly revert any attempts to change it to dark
                  const observer = new MutationObserver((mutations) => {
                    mutations.forEach((mutation) => {
                      if (mutation.attributeName === 'data-theme') {
                        if (document.documentElement.getAttribute('data-theme') !== 'light') {
                          document.documentElement.setAttribute('data-theme', 'light');
                        }
                      }
                    });
                  });
                  
                  // Start observing as soon as possible
                  observer.observe(document.documentElement, { attributes: true });
                  
                  // Also handle the body tag just in case
                  document.addEventListener("DOMContentLoaded", () => {
                    document.body.setAttribute('data-theme', 'light');
                    observer.observe(document.body, { attributes: true });
                  });
                </script>
                <style>
                  /* Fallback visual overrides just to be safe */
                  :root { color-scheme: light !important; }
                  body, html, .xblock-iframe-content {
                    background-color: #ffffff !important;
                  }
                </style>
                \"\"\"
                
                if '</head>' in content:
                    content = content.replace('</head>', injection + '\n</head>')
                    response.content = content.encode('utf-8')
                    if 'Content-Length' in response:
                        response['Content-Length'] = str(len(response.content))
            except Exception:
                pass 

        return response

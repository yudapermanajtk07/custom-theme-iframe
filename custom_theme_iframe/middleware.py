class ForceLightModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/xblock/') and 'text/html' in response.get('Content-Type', ''):
            try:
                content = response.content.decode('utf-8')
                
                # 1. Clean up Indigo theme dark classes directly from the HTML source
                content = content.replace('indigo-dark-theme', '')
                
                # 2. Inject Script and CSS to force light mode logically and visually
                injection = """
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
                      // Also watch for class changes in body
                      if (mutation.attributeName === 'class' && document.body) {
                        if (document.body.classList.contains('indigo-dark-theme')) {
                           document.body.classList.remove('indigo-dark-theme');
                        }
                      }
                    });
                  });
                  
                  // Start observing as soon as possible
                  observer.observe(document.documentElement, { attributes: true });
                  
                  // Also handle the body tag
                  document.addEventListener("DOMContentLoaded", () => {
                    document.body.setAttribute('data-theme', 'light');
                    document.body.classList.remove('indigo-dark-theme');
                    observer.observe(document.body, { attributes: true });
                  });
                </script>
                <style>
                  /* Fallback visual overrides just to be safe */
                  :root { color-scheme: light !important; }
                  body, html, .xblock-iframe-content {
                    background-color: #ffffff !important;
                    color: #000000 !important;
                  }
                  .xblock-iframe-content p, .xblock-iframe-content div, .xblock-iframe-content span, .xblock-iframe-content h1, .xblock-iframe-content h2, .xblock-iframe-content h3 {
                    color: #000000;
                  }
                </style>
                """
                
                if '</head>' in content:
                    content = content.replace('</head>', injection + '\n</head>')
                    response.content = content.encode('utf-8')
                    if 'Content-Length' in response:
                        response['Content-Length'] = str(len(response.content))
            except Exception:
                pass 

        return response

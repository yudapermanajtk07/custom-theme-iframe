class ForceLightModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Intercept only HTML responses on XBlock iframe routes
        if request.path.startswith('/xblock/') and 'text/html' in response.get('Content-Type', ''):
            try:
                content = response.content.decode('utf-8')
                
                # CSS override to force light background and dark text
                style = \"\"\"
                <style>
                  /* Force light mode in iframe */
                  :root { color-scheme: light !important; }
                  body, html, .xblock-iframe-content {
                    background-color: #ffffff !important;
                    color: #0B1F3F !important;
                  }
                  /* Force text color for generic containers */
                  .xblock-iframe-content p, .xblock-iframe-content div, .xblock-iframe-content span {
                    color: #0B1F3F;
                  }
                </style>
                \"\"\"
                
                # Inject right before </head>
                if '</head>' in content:
                    content = content.replace('</head>', style + '\n</head>')
                    response.content = content.encode('utf-8')
                    # Update Content-Length header so it doesn't break transmission
                    if 'Content-Length' in response:
                        response['Content-Length'] = str(len(response.content))
            except Exception:
                pass # Fail gracefully

        return response

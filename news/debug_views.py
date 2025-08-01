from django.http import HttpResponse
from django.shortcuts import render

def debug_password_reset(request):
    """Debug view to test password reset template loading"""
    return HttpResponse("""
    <html>
    <head><title>Debug Password Reset</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1 style="color: red;">🔍 DEBUG VIEW WORKING</h1>
        <p><strong>This is our custom debug view for password reset.</strong></p>
        <p>If you see this, it means:</p>
        <ul>
            <li>Our URL routing is working</li>
            <li>Django is loading our custom view</li>
            <li>But the template loading might be broken</li>
        </ul>
        <hr>
        <p>Next step: Check template loading...</p>
    </body>
    </html>
    """)

def debug_template_test(request):
    """Test if we can render our custom template"""
    try:
        return render(request, 'registration/password_reset_form.html')
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1 style="color: red;">Template Loading Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Django cannot find or load the password_reset_form.html template.</p>
        </body>
        </html>
        """)

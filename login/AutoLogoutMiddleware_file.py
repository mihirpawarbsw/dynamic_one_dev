import time
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Timeout value in seconds (1 minute for testing)
        timeout = 15 * 60  
        if request.user.is_authenticated:
            current_time = time.time()
            last_activity = request.session.get('last_activity', current_time)
            
            # Check if the timeout has been exceeded
            if current_time - last_activity > timeout:
                logout(request)
                return redirect(settings.LOGOUT_REDIRECT_URL)
            else:
                # Update the last activity time
                request.session['last_activity'] = current_time

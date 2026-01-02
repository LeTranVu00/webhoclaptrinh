from django.conf import settings
from django.contrib.auth import login as auth_login
from allauth.account import signals
from django.dispatch import receiver


@receiver(signals.email_confirmed)
def email_confirmed_auto_login(sender, request, email_address, **kwargs):
    """Dev-only: when an email is confirmed, log the user in if DEBUG=True.
    This is a helper for testing; do NOT enable in production.
    """
    # Only activate in dev when explicitly allowed
    if not (getattr(settings, 'DEBUG', False) and getattr(settings, 'DEV_AUTO_LOGIN_ON_CONFIRM', False)):
        return
    user = email_address.user
    if not user:
        return
    backend = None
    try:
        backend = settings.AUTHENTICATION_BACKENDS[0]
    except Exception:
        backend = 'django.contrib.auth.backends.ModelBackend'
    setattr(user, 'backend', backend)
    try:
        auth_login(request, user)
    except Exception:
        # best effort for dev; ignore failures
        pass

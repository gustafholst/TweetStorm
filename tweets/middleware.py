class HeadersForGreatJustice:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Disables eval and inline resource (e.g. inline CSS/JS) and
        # whitelists self (a source with the same scheme/host/port combination,
        # with "same" being same as where this policy is defined), as the only
        # allowed source that resources can be loaded from
        response['Content-Security-Policy'] = "default-src 'self'"
        # Don't leak referrer information to external sites
        response['Referrer-Policy'] = "same-origin"

        return response

class HeadersForGreatJustice:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Disables eval and inline resource (e.g. inline CSS/JS) and
        # whitelists self (a source with the same scheme/host/port combination,
        # with "same" being same as where this policy is defined), as the only allowed
        # source that resources can be loaded from
        response['Content-Security-Policy'] = "default-src: 'self'"
        # Don't leak referrer information
        response['Referrer-Policy'] = "no-referrer"

        # The following two might not (?) be very necessary anymore but they also don't hurt.
        # Descriptions from https://securityheaders.com/ by Scott Helme

        # "X-Content-Type-Options stops a browser from trying to MIME-sniff the content
        # type and forces it to stick with the declared content-type. The only valid value
        # for this header is "X-Content-Type-Options: nosniff"."
        response['X-Content-Type-Options'] = "nosniff"
        # " X-XSS-Protection sets the configuration for the cross-site scripting filters
        # built into most browsers. The best configuration is "X-XSS-Protection: 1; mode=block"."
        response['X-XSS-Protection'] = "1; mode=block"
        return response

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class SecurityHeadersMiddleware:
    """Apply baseline security headers to API responses."""

    def __init__(self, app: ASGIApp, app_env: str = "dev") -> None:
        self.app = app
        self.app_env = app_env.lower()

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        async def send_wrapper(message: Message) -> None:
            if message["type"] != "http.response.start":
                await send(message)
                return

            response = Response()
            response.raw_headers = list(message["headers"])
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("Referrer-Policy", "no-referrer")
            response.headers.setdefault(
                "Permissions-Policy",
                "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
                "microphone=(), payment=(), usb=()",
            )

            path = request.url.path
            if path == "/health" or path.startswith("/api/"):
                csp = (
                    "default-src 'none'; frame-ancestors 'none'; "
                    "base-uri 'none'; form-action 'none'"
                )
                response.headers.setdefault(
                    "Content-Security-Policy",
                    csp,
                )

            if self.app_env == "prod" and request.url.scheme == "https":
                response.headers.setdefault(
                    "Strict-Transport-Security",
                    "max-age=31536000; includeSubDomains",
                )

            message["headers"] = response.raw_headers
            await send(message)

        await self.app(scope, receive, send_wrapper)

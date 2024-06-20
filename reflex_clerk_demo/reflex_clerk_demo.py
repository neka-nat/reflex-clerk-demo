import reflex as rx

import reflex_clerk as clerk
import reflex_clerk.clerk_client
from dotenv import load_dotenv

load_dotenv()

class State(rx.State):
    """The app state."""
    ...


@rx.page("/")
def index() -> rx.Component:
    return (
        clerk.clerk_provider(
            rx.center(
                rx.vstack(
                    rx.heading("Reflex Clerk Demo!", size="9"),
                    clerk.signed_out(
                        rx.button(
                            clerk.sign_in_button(force_redirect_url="/test-auth"),
                            size="4",
                            color_scheme="gray",
                            background="black"
                        ),
                    ),
                    clerk.signed_in(
                        rx.button(
                            "test-auth",
                            on_click=rx.redirect("/test-auth"),
                        )
                    ),
                    align="center",
                    spacing="7",
                ),
                height="100vh",
            ),
        )
    )


@rx.page("/test-auth")
def auth_required_page():
    return clerk.clerk_provider(
        rx.center(
            rx.vstack(
                rx.heading("Auth required test"),
                clerk.signed_in(
                    rx.cond(
                        clerk.ClerkState.user.has_image,
                        rx.chakra.avatar(
                            src=clerk.ClerkState.user.image_url,
                            name=clerk.ClerkState.user.first_name,
                            size="xl",
                        ),
                    )
                ),
                clerk.protect(
                    rx.fragment("You are logged in as ", clerk.ClerkState.user.first_name),
                    fallback=clerk.redirect_to_sign_in()
                ),
                clerk.signed_in(
                    rx.button(
                        clerk.sign_out_button(),
                        size="4",
                        color_scheme="gray",
                        background="black"
                    )
                ),
            ),
       ),
    )


app = rx.App()
reflex_clerk.install_signin_page(app)

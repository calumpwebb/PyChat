from pydux.combine_reducers import combine_reducers

from state.reducers.app import app
from state.reducers.errors import errors
from state.reducers.invite import invite
from state.reducers.login import login
from state.reducers.signup import signup
from state.reducers.welcome import welcome

pychat_app = combine_reducers(
    {
        "app": app,
        "welcome": welcome,
        "signup": signup,
        "errors": errors,
        "login": login,
        "invite": invite,
    }
)

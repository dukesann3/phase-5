import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import Login from "./components/Login";
import PostPage from "./components/post/PostBlock";
import UserProfilePage from "./components/user/UserProfilePage";
import Welcome from "./components/Welcome";
import CreateAccount from "./components/user/CreateAccount";
import FriendsList from "./components/friend/FriendsList";
import Profile from "./components/profile/Profile";
import Settings from "./components/Settings";

// import Tester from "./components/Tester";

const routes = [
    {
        path: '/',
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: '/',
                element: <Welcome />
            },
            {
                path: '/login',
                element: <Login />
            },
            {
                path: '/home/:user_id',
                element: <Home />
            },
            {
                path: '/post/:postid',
                element: <PostPage />
            },
            {
                path: '/profile',
                element: <UserProfilePage />
            },
            {
                path: '/create_an_account',
                element: <CreateAccount />
            },
            {
                path: '/friendslist',
                element: <FriendsList />
            },
            {
                path: `/user/:userid/profile`,
                element: <Profile />
            },
            {
                path: '/settings',
                element: <Settings />
            }
        ]   
    }
]

export default routes;
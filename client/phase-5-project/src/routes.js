import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import Login from "./components/Login";
import Message from "./components/Message";
import PostPage from "./components/Postpage";
import UserProfilePage from "./components/UserProfilePage";

import Tester from "./components/Tester";

const routes = [
    {
        path: '/',
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: '/makeforward slash after testing redux',
                element: <Login />
            },
            {
                path: '/home/:username',
                element: <Home />
            },
            {
                path: '/message/:username',
                element: <Message />
            },
            {
                path: '/post/:postid',
                element: <PostPage />
            },
            {
                path: '/profile/:userid',
                element: <UserProfilePage />
            },
            {
                path: '/',
                element: <Tester />
            }
        ]   
    }
]

export default routes;
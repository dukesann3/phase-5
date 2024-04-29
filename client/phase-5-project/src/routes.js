import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import Login from "./components/Login";
import Message from "./components/Message";
import PostPage from "./components/Postpage";
import UserProfilePage from "./components/UserProfilePage";
import Welcome from "./components/Welcome";
import UserTest from "./components/UserTest";
import CreateAccount from "./components/CreateAccount";

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
            // {
            //     path: '/',
            //     element: <UserTest />
            // },
            {
                path: '/login',
                element: <Login />
            },
            {
                path: '/home/:user_id',
                element: <Home />
            },
            {
                path: '/message/:user_id',
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
            // {
            //     path: '/',
            //     element: <Tester />
            // },
            {
                path: '/create_an_account',
                element: <CreateAccount />
            }
        ]   
    }
]

export default routes;
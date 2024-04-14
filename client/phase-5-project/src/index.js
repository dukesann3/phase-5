import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { Provider } from "react-redux";
import routes from "./routes";
import store from "./app/store";

const router = createBrowserRouter(routes);
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Provider store={store}>
    <RouterProvider router={router}/>
  </Provider>
);


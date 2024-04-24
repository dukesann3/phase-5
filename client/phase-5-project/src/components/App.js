import { Outlet } from "react-router-dom";
import { Navbar } from "./Navbar";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { checkSession } from "../features/user/userLogged";
import Login from "./Login";

function App() {

  const dispatch = useDispatch()
  const loggedInUser = useSelector((store) => store.loggedInUser)

  useEffect(()=>{
    dispatch(checkSession())
  }, [])

  return (
    <>
      <Navbar />
      <h1>This is App</h1>
      {
        Object.keys(loggedInUser.value).length > 0 ? 
        <div>
          <h5>This is Outlet</h5>
          <h2>Testing...</h2>
          <p>{loggedInUser.value.username}</p>
          <Outlet />
        </div>
        :
        <Login />
      }
      <Outlet />
      <h1>This is Footer</h1>
    </>
  );
}

export default App;

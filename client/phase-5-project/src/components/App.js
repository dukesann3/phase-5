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
      <Outlet />
      <h1>This is Footer</h1>
    </>
  );
}

export default App;

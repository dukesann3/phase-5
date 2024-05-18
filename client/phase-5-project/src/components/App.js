import { Outlet } from "react-router-dom";
import { Navbar } from "./Navbar";
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { checkSession } from "../features/user-slice/user";

function App() {

  const dispatch = useDispatch()

  const loggedInUser = useSelector((store) => store.user.value)
  const userList = useSelector((store) => store.userList.value)
  const friends = useSelector((store) => store.friends.value)

  console.log(loggedInUser, userList, friends)

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

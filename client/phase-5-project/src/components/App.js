import { Outlet } from "react-router-dom";
import { Navbar } from "./Navbar";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { checkSession } from "../features/user-slice/user";
import Footer from "./Footer";
import "../CSS/parent.css"

function App() {

  const dispatch = useDispatch()

  useEffect(()=>{
    dispatch(checkSession())
  }, [])

  return (
    <>
      <Navbar />
      <Outlet />
      <Footer />
    </>
  );
}

export default App;

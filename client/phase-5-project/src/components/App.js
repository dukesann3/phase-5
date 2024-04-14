import { Outlet, Link, NavLink } from "react-router-dom";

function App() {
  return (
    <>
      <h1>This is App</h1>
      <div>
        <h5>This is Outlet</h5>
        <Outlet />
      </div>
      <h1>This is Footer</h1>
    </>
  );
}

export default App;

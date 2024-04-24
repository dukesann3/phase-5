import { useDispatch, useSelector } from "react-redux";

function UserProfilePage(){

    const loggedInUser = useSelector((store) => store.loggedInUser)
    console.log(loggedInUser)
    return(
        <>
        </>
    )
}

export default UserProfilePage;
import { useDispatch, useSelector } from "react-redux";

function UserProfilePage(){

    const loggedInUser = useSelector((store) => store.loggedInUser)
    const userValues = loggedInUser.value

    console.log(userValues._image_src)

    return(
        <>
            <h3>Profile Page</h3>
            <img src='/images/2_folder/2_profile_picture_folder/2_profile.jpg' />
            <span>{userValues.first_name}</span>
            <span>{userValues.last_name}</span>
            <span>{userValues.username}</span>
        </>
    )
}

export default UserProfilePage;

function UserProfile({user, open}){

    const {_image_src, first_name, last_name, username} = user

    console.log(_image_src)

    return(
        <>
            <h3>Profile Page</h3>
            <img src={_image_src} />
            <span>{first_name}</span>
            <span>{last_name}</span>
            <span>{username}</span>
            <button onClick={open}>Edit</button>
        </>
    )
}

export default UserProfile;
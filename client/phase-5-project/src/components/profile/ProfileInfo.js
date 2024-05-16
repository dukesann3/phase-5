import PostBlock from "../post/PostBlock"

function ProfileInfo({user, posts}){

    const {first_name, last_name, username, _image_src, id} = user

    return(
        <>
            <h4>Profile Page</h4>
            <img src={_image_src} />
            <span>{first_name}</span>
            <span>{last_name}</span>
            <span>{username}</span>
            {
                posts.map((post) => {
                    return <PostBlock key={post.id} post={post}/>
                })
            }
        </>
    )
}

export default ProfileInfo


function FriendBlock({friend}){

    const {first_name, last_name, username, status} = friend

    return(
        <>
            <p>Friend Block</p>
            <p>FIRST: {first_name}</p>
            <p>LAST: {last_name}</p>
            <p>USERNAME: {username}</p>
            <p>{status}</p>
        </>
    )
}

export default FriendBlock
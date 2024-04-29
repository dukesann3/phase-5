import { useSelector } from "react-redux"

export default function UseBlock({user}){

    const loggedInUser = useSelector((store) => store.loggedInUser.value)

    function sendFriendRequest(e){
        e.preventDefault()
        console.log("here?")
        fetch('/friendships/send_request', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sender_id: loggedInUser.id,
                reciever_id: user.id
            })
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Either the sender or reciever of the friend request does not exist")
            throw new Error("Network Error")
        })
        .then((r) => console.log(r))
        .catch((err) => console.log(err))
    }

    return(
        <>
            <span>First Name: {user.first_name}</span>
            <span>Last Name: {user.last_name}</span>
            <span>Username: {user.username}</span>
            <button onClick={sendFriendRequest}>Send Friend Request</button>
        </>
    )
}
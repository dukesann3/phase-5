import { useDispatch } from "react-redux"
import { deleteNotification } from "../../features/user-slice/user"

export default function NotificationBlock({notification}){

    const dispatch = useDispatch()

    const noteInfoToDelete = {
        id: notification.value.id,
        type: notification.type
    }

    //play around with this function and if it works, replace it with redux

    const onResponseChange = (response, e) => {
        e.preventDefault()
        fetch('/friendships/send_request', {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                friend_request_response: response,
                friend_request_id: notification.value.friendship[0].id
            })
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 400) throw new Error(r.json())
            throw new Error(r.json())
        })
        .then((r) => {
            console.log(r)
            window.location.reload()
        })
        .catch((err) => console.log(err))
    }

    return(
        <>
            <span>Notification Dayo!</span>
            <p>{notification.type}</p>
            <p>{notification.value.text}</p>
            {
                notification.type === "friend_request_notifications"?
                <>
                    <button onClick={(e) => onResponseChange("accepted", e)}>Accept</button>
                    <button onClick={(e) => onResponseChange("rejected", e)}>Reject</button>
                </>
                :
                <button onClick={() => dispatch(deleteNotification(noteInfoToDelete))}>DELETE</button>
            }
        </>
    )
}
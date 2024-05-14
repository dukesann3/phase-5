import { useDispatch } from "react-redux"
import { deleteNotification, respondToFriendRequest } from "../../features/user-slice/user"

export default function NotificationBlock({notification}){

    const dispatch = useDispatch()

    const noteInfoToDelete = {
        id: notification.value.id,
        type: notification.type
    }

    //play around with this function and if it works, replace it with redux

    const onFriendRequestResponse = (response) => {
        const friendship_id = notification.value.friendship_id
        dispatch(respondToFriendRequest(friendship_id, response))
    }

    return(
        <>
            <span>Notification Dayo!</span>
            <p>{notification.type}</p>
            <p>{notification.value.text}</p>
            {
                notification.type === "friend_request_notifications"?
                <>
                    <button onClick={() => onFriendRequestResponse("accepted")}>Accept</button>
                    <button onClick={() => onFriendRequestResponse("rejected")}>Reject</button>
                </>
                :
                <button onClick={() => dispatch(deleteNotification(noteInfoToDelete))}>DELETE</button>
            }
        </>
    )
}
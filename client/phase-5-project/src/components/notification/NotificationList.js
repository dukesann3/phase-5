import { useSelector } from "react-redux"
import { notificationSelector } from "../../features/user-slice/user"
import NotificationBlock from "./NotificationBlock"

export default function NotificationList(){

    const userInfo = useSelector((store) => store.user)
    const notifications = useSelector(notificationSelector)

    return(
        <>
            <span>Notification List</span>
            {   Object.keys(userInfo.value).length !== 0 ?
                notifications.map((notification) => {
                    //try to distinguish between friend request notification and post like/ comment like notification
                    return <NotificationBlock key={notification.id} notification={notification}/>
                })
                :
                null
            }
        </>
    )
}
import NotificationList from "./notification/NotificationList";
import UserList from "./user/UserList";
import PostList from "./post/PostList";
import "../CSS/home.css"

function Home(){

    return(
        <>
            <div className="home-grid-container">
                <div className="grid-home-item-left">
                    <UserList className="home-grid-item-left-top"/>
                    <PostList className="home-grid-item-left-bottom"/>
                </div>
                <NotificationList className="grid-home-item-right"/>
            </div>
        </>
    )
}

export default Home;
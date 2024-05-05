import CommentBlock from "./CommentBlock"
import CreateComment from "./CreateComment"

export default function CommentList({comments, post_id}){
    return(
        <>
            <h6>This is a comment list</h6>
            {comments.map((comment) => {
                return <CommentBlock key={post_id+comment.id} comment={comment}/>
            })}
            <CreateComment post_id={post_id}/>
        </>
    )
}
import CommentList from "../comment/CommentList"
import { useSelector, useDispatch } from "react-redux"
import { patchPost, deletePost, postPostLike, deletePostLike} from "../../features/post-slice/allPosts"
import { useState } from "react"
import { useFormik } from "formik"
import { NavLink } from "react-router-dom"
import 'semantic-ui-css/semantic.min.css'
import { CardMeta, CardHeader, Card, CardDescription,
    Image, Button, Form, FormField, FormGroup } from "semantic-ui-react"
import "../../CSS/postblock.css"
import "../../CSS/postedit.css"

export default function PostBlock({post}){

    const [editMode, setEditMode] = useState(false)
    const enterEditMode = () => setEditMode(true)
    const exitEditMode = () => setEditMode(false)

    const userInfo = useSelector((store) => store.user.value)
    const dispatch = useDispatch()
    
    const {caption, location, created_at, updated_at, _image_src, comments, id, user_id, post_likes, user} = post

    const getModifiedValues = (values, initialValues) => {
        let modifiedValues = {};
      
        if (values) {
            Object.entries(values).forEach((entry) => {
            let key = entry[0];
            let value = entry[1];
      
            if (value !== initialValues[key] || (key === "image_uri" && values["image_uri"].length > 0)) {
                modifiedValues[key] = value;
            }
          });
        }
      
        return modifiedValues;
    };

    const liked_posts = () => {
        let posts = []
        for(let i = 0; i < post_likes.length; i++){
            if(post_likes[i].isLiked === true){
                posts.push(post_likes[i])
            }
        }
        return posts.length
    }

    const isLikedByUser = () => {
        for(const like of post_likes){
            if(like.user_id === userInfo.id){
                return {
                    isLiked: true,
                    post_like_id: like.id
                }
            }
        }
        return {
            isLiked: false,
            post_like_id: -1
        }
    }

    const formik = useFormik({
        initialValues: {
            image_uri: "",
            location: "",
            caption: ""
        },
        onSubmit: (value) => {
            const modifiedValue = getModifiedValues(value, formik.initialValues)
            dispatch(patchPost(modifiedValue, id))
            exitEditMode()
        }
    })

    function onImageChange(e){
        try{
            const reader = new FileReader()
            reader.readAsDataURL(e.target.files[0])
            reader.addEventListener("load", () => {
                const uri = reader.result
                formik.values.image_uri = uri
            })
        }
        catch(error){
            console.log(error)
        }
    }

    function pressLike(){
        const postLikeStatus = isLikedByUser()
        if(postLikeStatus.isLiked){
            dispatch(deletePostLike(postLikeStatus.post_like_id))
        }
        else{
            dispatch(postPostLike({
                post_id: id,
                isLiked: true
            }))
        }
    }

    console.log(userInfo.id, user_id)

    return(
        <div>
            {
            editMode ?
            <>
                <Form className="post-edit-form" onSubmit={formik.handleSubmit}>
                    <div className="post-edit-word-container"><span>Post Edit</span></div>
                    <FormField>
                        <label>Image</label>
                        <input 
                        type="file"
                        id="image_uri"
                        onChange={onImageChange}
                        placeholder="image"
                        />
                    </FormField>

                    <FormGroup>
                        <FormField>
                            <label>Text</label>
                            <input
                            type="text"
                            id="location"
                            onChange={formik.handleChange}
                            value={formik.values.location}
                            placeholder="location"
                            />
                        </FormField>

                        <FormField>
                            <label>Caption</label>
                            <input
                            type="text"
                            id="caption"
                            onChange={formik.handleChange}
                            value={formik.values.caption}
                            placeholder="caption"
                            />
                        </FormField>
                    </FormGroup>


                    <input 
                    type="submit"
                    />
                    <button onClick={exitEditMode}>exit edit mode</button>
                </Form>
            </>
            :
            <Card fluid={true}>
                <div className="post-container">
                    <Image className="post-image" src={_image_src}/>
                    <CardMeta><span className="post-date">Created at: {created_at}</span></CardMeta>
                    <CardMeta><span className="post-date">Updated at: {updated_at}</span></CardMeta>
                    <CardMeta>{location}</CardMeta>
                    <div className="post-caption-block">
                        <CardHeader><h3>{caption}</h3></CardHeader>
                    </div>
                    <CardHeader>
                        <NavLink to={userInfo.id == user_id ? `/profile` : `/user/${user_id}/profile`}>
                            <span>Post By: {user.username}</span>
                        </NavLink>
                    </CardHeader>
                    <div className="post-like-heart">
                        <CardDescription>❤</CardDescription>
                        <CardDescription>{liked_posts()}</CardDescription>
                        <Button className="post-like-button" onClick={() => pressLike()}>Like</Button>
                    </div>
                    <div className="delete-edit-post-container">
                    {
                        userInfo.id === user_id?
                        <div className="ui two buttons">
                            <Button basic color='red' onClick={() => dispatch(deletePost(id))}>DELETE</Button>
                            <Button basic color='yellow' onClick={enterEditMode}>EDIT</Button>
                        </div>
                        :
                        null
                    }
                    </div>
                    <CommentList comments={comments} post_id={id}/>
                </div>
            </Card>
            }
        </div>
    )
}


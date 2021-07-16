
const onSetPostLikeCount = async (likeCount) => {
    const postLikeCountOfUser = document.getElementById('user-like-count');
    postLikeCountOfUser.innerHTML = `내가 좋아하는 글 : ${likeCount}개 `;
  }
  
  const onClickLikeButton = async (postId) => {
    const postLikeButton = document.getElementById(`${postId}-like-button`);
    const response = await axios.get(`/posts/${postId}/like/`);
    postLikeButton.setAttribute('data-badge', response.data.postLikeCount);
  
    if(response.data.postLikeOfUser == 1) {
      postLikeButton.innerHTML = "favorite";
    } else {
      postLikeButton.innerHTML = "favorite_border";
    }
    onSetPostLikeCount(response.data.userLikeCount);
  }
  
  const getTagElement = (tagContent, tagId) => {
    let newTagElement = document.createElement('a');
    newTagElement.setAttribute('href', `/tags/${tagId}/`);
    newTagElement.innerHTML = tagContent + "&nbsp;";
    return newTagElement;
  }
  
  const onAddTag = async () => {
    const tagInputElement = document.getElementById("tag-input");
    if(tagInputElement.value) {
      let data = new FormData();
      data.append("content", tagInputElement.value);
      const response = await axios.post(`/tags/new/`, data);
      const tagElement = getTagElement(tagInputElement.value, response.data.tagId);
      document.getElementById("tag-list").appendChild(tagElement);
      tagInputElement.value = '';
    }
  }
  
  const onDeletePost = async (postId) => {
    const confirmDeleteFeed = confirm('정말 삭제하시겠습니까?');
    
    if(confirmDeleteFeed) {
      const response = await axios.delete(`/posts/${postId}/delete/`);
      const post = document.getElementById(`post-${postId}`);
      post.remove();
      onSetPostLikeCount(response.data.postLikeCount);
    }
  }

  const onClickCategory=async (category)=>{
    const pets= document.getElementsByClassName('animal');
    let id='p'+category+"-pet-rank";
    if (category==0){
      for(var i=1; i<=pets.length; i+=1){
        pets[i].style.display='block';
      }
    }else{
      for (var i=0;i<pets.length;i+=1){
        if (pets[i].id==id){
          pets[i].style.display = 'block';
        }
        else{
          pets[i].style.display = 'none';
        }
      }
    }
    
  }
  const onSetCommentCount = (commentCount) => {
    const commentCountElement = document.getElementById('comment-count');
    commentCountElement.innerHTML = `<strong>댓글이 ${commentCount}개 있습니다</strong>`;
  }
  
  const getCommentElement = (postId, commentId, commentCount, comment, createdTime, author) => {
    var commentElement = document.createElement('p');
    commentElement.id = `post${postId}-comment${commentId}`;
    commentElement.innerHTML = `${author}: ${comment} &nbsp; &nbsp; ${createdTime}
                                <a id="comment${commentId}-like-button" onclick="onLikeComment(${commentId})">
                                ${ commentCount } Likes </a>
                                <a onclick="onDeleteComment(${postId}, ${commentId})">댓글 삭제</a>`  
    return commentElement;
  }
  
  const onAddComment = async (postId) => {
    const commentInputElement = document.getElementById(`post${postId}-comment-input`);
    console.log(commentInputElement)
    const data = new FormData();
    data.append("content", commentInputElement.value);
    const response = await axios.post(`/posts/${postId}/comments/`, data);
    const { commentId, commentCount, commentLikeCount, createdTime, author } = response.data;
    const commentElement = getCommentElement(postId, commentId, commentLikeCount, commentInputElement.value, createdTime, author);
    document.getElementById(`${postId}-comment-list`).appendChild(commentElement);
    onSetCommentCount(commentCount);
    commentInputElement.value = '';
  }

 
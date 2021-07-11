const onLikePost = async (postId) => {
    const postLikeButton = document.getElementById(`show-${postId}-like-button`);
    const response = await axios.get(`/posts/${postId}/like/`);
    postLikeButton.innerHTML = `${response.data.postLikeCount} Likes`;
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
    const data = new FormData();
    data.append("content", commentInputElement.value);
    const response = await axios.post(`/posts/${postId}/comments/`, data);
    const { commentId, commentCount, commentLikeCount, createdTime, author } = response.data;
    const commentElement = getCommentElement(postId, commentId, commentLikeCount, commentInputElement.value, createdTime, author);
    document.getElementById(`${postId}-comment-list`).appendChild(commentElement);
    onSetCommentCount(commentCount);
    commentInputElement.value = '';
  }
  
  const onLikeComment = async (commentId) => {
    const CommentLikeButton = document.getElementById(`comment${commentId}-like-button`);
    const response = await axios.get(`/posts/${commentId}/commentlike/`);
    const commentLikeCount = response.data.commentLikeCount;
    CommentLikeButton.innerHTML = `${commentLikeCount} Likes`;
  }
  
  const onDeleteComment = async (postId, commentId) => {
    if(confirm('댓글을 정말 삭제하시겠습니까?')) {
      const response = await axios.delete(`/posts/${postId}/comments/${commentId}/`);
      const commentElement = document.getElementById(`post${postId}-comment${commentId}`);
  
      const commentCount = response.data.commentCount;
      onSetCommentCount(commentCount);
      commentElement.remove();
    }
  }
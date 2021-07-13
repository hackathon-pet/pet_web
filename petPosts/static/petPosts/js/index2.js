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
      if (category==0){
        
      }
  }
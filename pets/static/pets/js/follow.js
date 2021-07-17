const follow = async () => {
    

      const response = await axios.delete(`/posts/${postId}/delete/`);
      const post = document.getElementById(`post-${postId}`);
      post.remove();
      onSetPostLikeCount(response.data.postLikeCount);

  }
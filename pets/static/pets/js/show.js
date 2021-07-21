const follow = async (petID) => {
    
    const followers = document.getElementById(`${petID}-followers`);
    const response = await axios.get(`/pets/${petID}/follow/`);
    const follow_count = response.data.follow_count;
    followers.innerHTML = `${follow_count} followers`;

  }

  const onDeletePet = async (petID) => {

    const confirmDeletePet = confirm('펫을 정말 삭제하시겠습니까?');
    if(confirmDeletePet) {
      const response = await axios.delete(`/pets/${petID}/delete/`);
      location.replace(`/accounts/myinfo/`);
    }
  }
  const nofollow=async() =>{
    alert('팔로우를 하려면 회원가입 또는 로그인을 하세요');
  }
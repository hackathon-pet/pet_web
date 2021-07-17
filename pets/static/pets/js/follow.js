const follow = async (petID) => {
    
    const followers = document.getElementById(`${petID}-followers`);
    const response = await axios.get(`/pets/${petID}/follow/`);
    const follow_count = response.data.follow_count;
    followers.innerHTML = `${follow_count} followers`;

  }
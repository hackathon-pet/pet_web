class Pet(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=20, blank=True)
  PET_CHOICES = (
      ('p1', '강아지'),
      ('p2', '고양이'),
      ('p3', '햄스터'),
      ('p4', '포유류'),
      ('p5', '조류'),
      ('p6', '어류'),
      ('p7', '파충류'),
      ('p8', '거미/전갈')
  )
  category = models.CharField(max_length=2, choices=PET_CHOICES)
  #age?
  introduction = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='images/',blank=True, null=True)
  follow_users = models.ManyToManyField(User, blank=True, related_name='following_pets', through='Follow')

  def __str__(self):     
    return f'id={self.id}, name={self.name}'
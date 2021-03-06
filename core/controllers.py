from state_predictor import *
from comm import *

class AuthorizationController(StatePredictor):
	
	def __init__(self, minifig_detector, rooms_auth, update_interval = 10):
		self.minifig_detector = minifig_detector
		self.rooms_auth = rooms_auth
		
		self.rooms = []
		for r in self.rooms_auth.values():
			self.rooms.extend(r)
		self.rooms = list(set(self.rooms))
		self.rooms_auth_status = {}
		
		for r in self.rooms:
			self.rooms_auth_status[r] = False
		
		states = {
			0 : State('do nothing', 0),
			1 : State('open door', 1),
			2 : State('close door', 2)	
		}
		self.update_interval = update_interval
		super(AuthorizationController, self).__init__(states=states, sensors=[], update_interval=update_interval)

	def update(self):
		
		for lbl in self.minifig_detector.class_labels:
			if self.minifig_detector.status[lbl] >= 1:
				for r in self.rooms[lbl]:
					self.rooms_auth_status[r] = True	
		
		for r in self.rooms:
			if self.rooms_auth_status[r] == True:
				AuthorizationController.open_door(r)
			else:
				AuthorizationController.close_door(r)
		
		self.reset_auth()
			
	def reset_auth(self):
		for r in self.rooms:
			self.rooms_auth_status[r] = False	
		
	@staticmethod		
	def open_door(x):
		pass
	
	@staticmethod	
	def close_door(x):
		pass
		
class EntranceController(StatePredictor):
	
	def __init__(self, minifig_detector, update_interval=10):
		self.minifig_detector = minifig_detector
		self.entrance_id = entrance_id
		states = {
			0 : State('do nothing', 0)
			1 : State('open entrance', 1)
			2 : State('close entrance', 2)
		}
		states[1].addSubscriber(AuthorizationController.open_door)
		states[2].addSubscriber(AuthorizationController.close_door)
		super(EntranceController, self).__init__(states=states, sensors = [], update_interval = update_interval)
		
	def update(self):
		
		if self.minifig_detector.number_of_people > 0:
			AuthorizationController.open_door(self.entrance_id)
			time.sleep(update_interval)
			AuthorizationController.close_door(self.entrance_id)
		
class PartyModeController(StatePredictor):
	
	def __init__(self, minifig_detector, music_preferences, number_of_people_threshold = 4, update_interval = 10):
		self.minifig_detector = minifig_detector
		self.music_preferences = music_preferences
		self.number_of_people_threshold = number_of_people_threshold
		states = {
			0 : State('do nothing', 0)
			1 : State('lets party', 1)
		}
		states[1].addSubscriber(self.party_rock())
		super(PartyModeController, self).__init__(states=states, sensors= [], update_interval = update_interval)
		cmd("export SPOTIPY_CLIENT_ID='db13c5c481574855b69a6209bdffc279'")
		cmd("export SPOTIPY_CLIENT_SECRET='ee74200a30754633baff860d4c0546f9'")
		cmd("export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'")
		
		scope = 'user-library-read'
		username="Giannhs Daras"
		try:
			token = util.prompt_for_user_token(username, scope)
		except:
			raise Exception('Error on spotify connection')

		assert(token)
		self.spotipy = spotipy.Spotify(auth=token)
			
		self.music_queries = {}
		self.tracks = {}
		for lbl in self.music_preferences.keys():
			self.music_queries[lbl] = []	
			for track in self.music_preferences[lbl]:
				results = self.spotipy.search( q=track, limit=1)
				t = results['tracks']['items']
				self.music_queries[lbl].append(t)
				self.tracks[t] = 0
			
	def update(self):
		
		if self.minifig_detector.number_of_people >= self.number_of_people_threshold:
			self.party_rock()
			
	def party_rock(self):
		
		for lbl in self.minifig_detector.class_labels:
			if self.minifig_detector.status[lbl] >= 1:
				self.tracks[self.music_queries[lbl]] += 1
		
		t = max(zip(self.tracks.keys(), self.tracks.values()), key = lambda x : x[1])[0]		
		result_url = t['preview_url']			
		webbrowser.open_new(result_url)	
				
class EnergySaverController(StatePredictor):

    def __init__(self):
        states = {
            0 : State('do nothing',0),
            1 : State('show message',1)
        }
        self.timeon=0
        self.counter=0
        states[1].addSubscriber(EnergySaverController.showmessage)
        sensors = [ledarray]
        super(EnergySaverController, self).__init__(states, sensors,update_interval=1)

    def getData(self):
        x = np.array([])
        for sensor in self.sensors:
            d = sensor.getData()
            x = np.append(x, d)
        return x 
        
    def update(self):
        """ Update NN """

        print 'Updating'

        x = self.getData()
        self.timeon += sum(x)
        self.counter=self.counter+1
        self.timeon=normalize(self.timeon, (l,r) = (0, 24))
        index = self.predict_next(self.timeon)

        # use softmax
        self.state = self.states[index]
        print ('New state: {0}'.format(self.states[index].name))

        # Retrain our model
        if self.counter == 15:
            self.counter =0
            print 'Retraining'
            y = keras.utils.to_categorical(index, self.num_classes)
            self.model.train_on_batch(np.array([self.timeon]), y)
            self.num_train += 1

        self.state.onActivation(self)


    def showmessage(self):
        print 'Daily usage exceeded'		

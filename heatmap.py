"""
Utility for retrieving Strava Heatmap Tiles for use in Gaia custom layers
"""

ride_heatmap_url = "https://www.strava.com/maps/global-heatmap?style=standard&terrain=false&sport=ride&gColor=hot&gOpacity=100#12.3/48.70698/-122.40974"
ski_heatmap_url = "https://www.strava.com/maps/global-heatmap?style=standard&terrain=false&sport=winter&gColor=blue&gOpacity=100#13.05/48.8305/-121.63693"

def format_url(url):
	"""Takes in a heatmap URL and returns bike and ski URLs formatted for Gaia"""
	bike = url
	if bike[:4] == "tms:": # Check for TMS prefix
		bike = bike[4:]
	bike = bike.replace("{switch:a,b,c}", "a")
	bike = bike.replace("{zoom}", "{z}")
	ski = bike.replace("ride", "winter")
	ski = ski.replace("hot", "blue")
	return (bike, ski)

def main():
	print("Navigate to the ride heatmap URL: " + ride_heatmap_url)
	url = input("Paste in the heatmap tile link you generated on the page: ")
	bike, ski = format_url(url)

	
	print("Ride heatmap:")
	print(bike)
	print("Ski heatmap:")
	print(ski)

if __name__ == '__main__':
	main()

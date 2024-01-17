"""
Utility for retrieving Strava Heatmap Tiles for use in Gaia custom layers
"""

ride_heatmap_url = "https://www.strava.com/heatmap#13.73/-122.38767/48.62712/hot/ride"
ski_heatmap_url = "https://www.strava.com/heatmap#13.73/-122.38767/48.62712/blue/winter"

def format_url(url):
	"""Takes in a heatmap URL with no TMS prefix and returns bike and ski URLs formatted for Gaia"""
	bike = url
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
	pass

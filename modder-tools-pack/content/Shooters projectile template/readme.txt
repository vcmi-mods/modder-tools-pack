Author: Macron1
Source: 
https://forum.vcmi.eu/t/macron1-topic-for-different-stuff/726/50

How to use it:
Custom-made suggested shooter grid template to make shooter projectiles draw correctly.
Create multi-layered graphics file in editor, put this file on top layer, and insert shooting climax frame of creature on second layer to suggest coordinates of projectile.

Note that Y axis coordinates are negative - if coords on grid is (30,40), than projectile climax coords must be like:

				"offset" :
				{
					"upperX" : 30,
					"upperY" : -40,
					"middleX" : 30,
					"middleY" : -40,
					"lowerX" : 30,
					"lowerY" : -40
				}
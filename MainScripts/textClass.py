from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
import argparse


class textDetect:
	def detect(self,image):
		def decode_predictions(scores, geometry):
			(numRows, numCols) = scores.shape[2:4]
			rects = []
			confidences = []
			for y in range(0, numRows):
				scoresData = scores[0, 0, y]
				xData0 = geometry[0, 0, y]
				xData1 = geometry[0, 1, y]
				xData2 = geometry[0, 2, y]
				xData3 = geometry[0, 3, y]
				anglesData = geometry[0, 4, y]
				for x in range(0, numCols):
					if scoresData[x] < 0.5:
						continue
					
					(offsetX, offsetY) = (x * 4.0, y * 4.0)
					angle = anglesData[x]
					cos = np.cos(angle)
					sin = np.sin(angle)
					h = xData0[x] + xData2[x]
					w = xData1[x] + xData3[x]
					endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
					endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
					startX = int(endX - w)
					startY = int(endY - h)
					rects.append((startX, startY, endX, endY))
					confidences.append(scoresData[x])
			return (rects, confidences)

		image = cv2.imread(image)
		orig = image.copy()
		(origH, origW) = image.shape[:2]
		(newW, newH) = (320, 320)
		rW = origW / float(newW)
		rH = origH / float(newH)
		image = cv2.resize(image, (newW, newH))
		(H, W) = image.shape[:2]
		layerNames = [
	        "feature_fusion/Conv_7/Sigmoid",
	        "feature_fusion/concat_3"]
		net = cv2.dnn.readNet("frozen_east_text_detection.pb")
		blob = cv2.dnn.blobFromImage(image, 7, (W, H),
	        (123.68, 116.78, 103.94), swapRB=True, crop=False)
		net.setInput(blob)
		(scores, geometry) = net.forward(layerNames)
		(rects, confidences) = decode_predictions(scores, geometry)
		boxes = non_max_suppression(np.array(rects), probs=confidences)
		results = []
		for (startX, startY, endX, endY) in boxes:
			startX = int(startX * rW)
			startY = int(startY * rH)
			endX = int(endX * rW)
			endY = int(endY * rH)
			dX = int((endX - startX) * 0.2)
			dY = int((endY - startY) * 0.2)
			startX = max(0, startX - dX)
			startY = max(0, startY - dY)
			endX = min(origW, endX + (dX * 2))
			endY = min(origH, endY + (dY * 2))
			roi = orig[startY:endY, startX:endX]
			config = ("-l tur --oem 3 --psm 10")
			text = pytesseract.image_to_string(roi, config=config)
			results.append(((startX, startY, endX, endY), text))

		results = sorted(results, key=lambda r:r[0][1])
		chrs = []
		keys = ["A","B","C","D","E","F","G","H","J","K","L","R"]
		for ((startX, startY, endX, endY), text) in results:
			print(text)
			if text in keys:
				chrs.append(text)


			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			output = orig.copy()
			cv2.rectangle(output, (startX, startY), (endX, endY),
		        (0, 0, 255), 2)
			cv2.putText(output, text, (startX, startY - 20),
		        	cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
			cv2.imshow("Text Detection", output)
			cv2.waitKey(0)



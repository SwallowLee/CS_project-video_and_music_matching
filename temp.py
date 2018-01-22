import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, simplejson as json


import cv2
vidcap = cv2.VideoCapture('video-1516194344.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1


subscription_key = '78fe6e39d7dc4e0e930e5e8cb743a749'

headers1 = {
    # Request headers.
       'Content-type': 'application/octet-stream',
}

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-type': 'application/octet-stream',
}

params = urllib.parse.urlencode({
        'subscription-Key': 'a1f7e0640f9f446daf56b0d41f9a6830',
})

params1 = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    'subscription-key': '78fe6e39d7dc4e0e930e5e8cb743a749',
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})

info = open(r'C:\Users\ASUS\.spyder-py3\image_info.json', "a")

i = 0
while i<count:
    body = "" 

    #load image

    filename = r'C:\Users\ASUS\.spyder-py3\frame%d.jpg'% i

    f = open(filename, "rb")

    body = f.read()

    f.close()
    if i%5 == 0:

        try:
            info.write ("###################### image %d ###########################\n"% i)
            # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
            #   URL below with "westcentralus".
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(data)
            info.write ("Response:")
            info.write (json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()
            
            # Execute the REST API call and get the response.
            conn1 = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn1.request("POST", "/vision/v1.0/analyze?%s" % params1, body, headers1)
            response1 = conn1.getresponse()
            data = response1.read()
            
            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed1 = json.loads(data)
            # info.write ("Response:")
            info.write (json.dumps(parsed1, sort_keys=True, indent=2))
            conn1.close()
            
        except Exception as e:
            print(e.args)
    i += 1
info.close()
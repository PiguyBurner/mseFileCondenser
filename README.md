# MSE File Condenser
This python script combines all the mse files into a single one so you don't have to manually.

## How to Use
0. install python if you don't have it already. Just google it.

1. Put all the mse-set files into the folder "place_mse_sets_here"

2. Put a template mse-set (it handles things default card frame, set symbol, etc) into "place_template_set_here"
**NOTE: Your template file will not have ANY of its cards copied over!!!

3. Open up your terminal and go to this location (`cd <wherever it's stored>/mseFileCondenser`)

4. type `python main.py` in the command line and run it

5. There are a few printouts; please listen to them!

6. Try opening `combined.mse-set` in MSE!
**NOTE: Whenever you run the condenser, it will clear out the output file, including the combined set you had previously! Listen to the printouts!

## Additional Notes

Please name your template file "template.mse-set" or else it won't work!

Also a reminder that none of the cards in there should be copied over.

If you are getting some things complaining, make sure you have the most recent MSE. 

If things still complain, try opening up and re-saving the files you want to combine. This was built with newer versions (as of 5/27/26) in mind; hopefully not much has changed and my error handling is adequate enough

I doubt this code is perfect but it succeeded in my testing so that's good enough for me. Hopefully it helps whoever needs it, and don't judge my code
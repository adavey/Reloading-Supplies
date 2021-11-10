import inspect
import WebSites


# Loop through classes defined in WebSites and execute method to check for product status
for name, obj in inspect.getmembers(WebSites):
    if inspect.isclass(obj) and obj.__module__=='WebSites':
        obj().process_site()
        print() # print a blank line between results

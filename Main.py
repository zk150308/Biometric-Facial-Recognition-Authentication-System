from uicontroller import UIController
from app_controller import AppController

app = AppController()
controller = UIController(app)
controller.mainloop()
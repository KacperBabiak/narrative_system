import pygame
import pygame_gui
from hotelgame import Game

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CHARACTER_INFO_WIDTH = 300
CHARACTER_INFO_HEIGHT = 100
MENU_BUTTON_WIDTH = 100
MENU_BUTTON_HEIGHT = 40
LIST_VIEW_WIDTH = 400
LIST_VIEW_HEIGHT = 400
OPTION_DROPDOWN_WIDTH = 150
OPTION_DROPDOWN_HEIGHT = 40

class GameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        
        
        # Menu buttons
        #self.item_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 500), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Items", manager=self.manager)
        #self.talk_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 500), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Talk", manager=self.manager)
        #self.fight_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 500), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Fight", manager=self.manager)
        #self.info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Info", manager=self.manager)
        self.next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Next", manager=self.manager)
        self.act_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 475), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Act", manager=self.manager)
        
        self.info_view = pygame_gui.elements.UITextBox("Info:", relative_rect=pygame.Rect((50, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager)
        self.text_view = pygame_gui.elements.UITextBox("Akcje:", relative_rect=pygame.Rect((550, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager)
        self.text_view.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        # Other menu
        
        actions = ["give","take","compliment","intimidate","attack","rest","take_care_of","work","spend_time_together",]
        self.action_dropdown = pygame_gui.elements.UIDropDownMenu(actions, relative_rect=pygame.Rect((50, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=actions[0], manager=self.manager)
        characters = ["actor","science","doctor","agent","tumblr"]
        self.character_dropdown = pygame_gui.elements.UIDropDownMenu(characters, relative_rect=pygame.Rect((250,475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=characters[0], manager=self.manager)
        items = ["food","money","weapon","book"]
        self.item_dropdown = pygame_gui.elements.UIDropDownMenu(items, relative_rect=pygame.Rect((450, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=items[0], manager=self.manager)

    def main_loop(self):
        planner = Game()

        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.next_button:
                        planner.check_all_goals()
                        planner.character_rotation()
                        planner.create_file()

                        action = planner.change_state()
                        self.text_view.append_html_text(action + "\n")

                        self.info_view.set_text(planner.print_state())
                    if event.ui_element == self.act_button:
                        arg_list = []
                        arg_list.append(self.action_dropdown.selected_option)
                        arg_list.append('mc')
                        arg_list.append(self.character_dropdown.selected_option)
                        arg_list.append(self.item_dropdown.selected_option)
                        
                        
                        planner.do_action(arg_list)
                        self.text_view.append_html_text(" ".join(arg_list) + "\n")

                        self.info_view.set_text(planner.print_state())
                        

                if event.type == pygame.QUIT:
                    running = False
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        pygame.quit()

def main():
    game = GameGUI()
    game.main_loop()

if __name__ == "__main__":
    main()

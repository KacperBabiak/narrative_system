import pygame
import pygame_gui
from game_files.main_game_loop import Main_Loop
from game_files.island_game_loop import Island_Loop

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
        
        self.planner = Island_Loop()
        self.sail_planner = Main_Loop() 
        
        # Menu buttons
        
        self.next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Next", manager=self.manager)
        self.escape_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Escape", manager=self.manager)
        self.act_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 475), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Act", manager=self.manager)
        


        self.info_view = pygame_gui.elements.UITextBox("Info:", relative_rect=pygame.Rect((50, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager)
        self.text_view = pygame_gui.elements.UITextBox("Akcje:", relative_rect=pygame.Rect((550, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager)
        self.text_view.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        # Other menu
        
        actions = ["ask_for_location","attack_for_location","ask_for_item","take_item","give_item","use_meds","rest", "attack", "spend_time_together"]
        self.action_dropdown = pygame_gui.elements.UIDropDownMenu(actions, relative_rect=pygame.Rect((50, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=actions[0], manager=self.manager)
        characters = self.planner.characters.copy()
        characters.remove('Mc')
        self.character_dropdown = pygame_gui.elements.UIDropDownMenu(characters, relative_rect=pygame.Rect((250,475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=characters[0], manager=self.manager)
        #items = ["Food","Gold","Fuel","Meds"]
        items = self.planner.items
        self.item_dropdown = pygame_gui.elements.UIDropDownMenu(items, relative_rect=pygame.Rect((450, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=items[0], manager=self.manager)

        #main loop

        self.info_view.set_text(self.sail_planner.print_islands())

        self.isl1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 50), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island1", manager=self.manager)
        self.isl2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 200), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island2", manager=self.manager)
        self.isl3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 350), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island3", manager=self.manager)


        self.act_button.hide()
        self.next_button.hide()
        self.escape_button.hide()
        self.text_view.hide()

    def main_loop(self):
        

        clock = pygame.time.Clock()
        running = True

        
        while running:
            time_delta = clock.tick(10) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    
                    if event.ui_element == self.next_button:
                        self.planner.check_escapes()
                        self.planner.character_rotation()
                        self.planner.create_file()

                        action = self.planner.change_state()
                        self.text_view.append_html_text(action + "\n")

                        
                        self.sail_planner.update_world(self.planner.world_state)

                        self.planner.create_goals()
                        self.info_view.set_text(self.planner.print_state())


                        
                    
                    elif event.ui_element == self.act_button:
                        arg_list = []
                        arg_list.append(self.action_dropdown.selected_option)
                        arg_list.append('Mc')
                        arg_list.append(self.character_dropdown.selected_option)
                        arg_list.append(self.item_dropdown.selected_option)
                        
                        
                        self.planner.do_action(arg_list)
                        self.text_view.append_html_text(" ".join(arg_list) + "\n")

                        self.info_view.set_text(self.planner.print_state())
                        
                    elif 'Isl' in event.ui_element.text  :
                        #creates a file with chosen chars
                        self.sail_planner.prepare_island(event.ui_element.text)
                        #reads the file
                        self.planner.init_world()

                        self.act_button.show()
                        self.next_button.show()
                        self.escape_button.show()
                        self.text_view.show()

                        self.isl1_button.hide()
                        self.isl2_button.hide()
                        self.isl3_button.hide()

                        self.text_view.clear()
                        self.info_view.set_text(self.planner.print_state())
                        
                    elif event.ui_element == self.escape_button:
                        
                        self.sail_planner.update_world(self.planner.world_state)
                        #nowe wyspy
                        self.sail_planner.create_islands()
                        self.info_view.set_text(self.sail_planner.print_islands())

                        #update world state
                        
                        self.isl1_button.show()
                        self.isl2_button.show()
                        self.isl3_button.show() 


                        self.act_button.hide()
                        self.next_button.hide()
                        self.escape_button.hide()
                        self.text_view.hide()

                        

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

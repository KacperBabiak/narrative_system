import pygame
import pygame_gui
from game_files.main_game_loop import Main_Loop
from game_files.island_game_loop import Island_Loop

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
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
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT),'E:\\Praca_magisterska\\narrative_system\\game_files\\assets\\theme.json')
        
        #self.screen.blit(pygame.image.load('game_files\\assets\\map_background.jpg'),(0,0))
        self.planner = Island_Loop()
        self.sail_planner = Main_Loop() 

        self.characters = self.planner.characters.copy()
        self.characters.remove('Mc')

        self.items = self.planner.items

        #panel WYSPY/////////////////////////////////////////////////////////////////////////////////////
        self.init_island_menu()
        
        #panel do podrózy między wyspami/////////////////////////////////////////////////////////////////////////////////////
        self.init_sail_menu()
        

        

        self.panel_sail.show()
        self.panel_island.hide()

    def init_sail_menu(self):
        self.panel_sail = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)), manager=self.manager)
        self.panel_sail_res = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT- 110)), manager=self.manager,container=self.panel_sail)
        self.panel_sail_com = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT- 110)), manager=self.manager,container=self.panel_sail)
        self.panel_sail_map = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT- 110)), manager=self.manager,container=self.panel_sail,element_id='map')
        self.panel_sail_res.hide()
        self.panel_sail_com.hide()
        self.panel_sail_map.show()

        #guziki wyboru menu
        self.res_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 620), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Resources", manager=self.manager,container=self.panel_sail)
        self.com_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 620), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Radio", manager=self.manager,container=self.panel_sail)
        self.map_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((725, 620), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Map", manager=self.manager,container=self.panel_sail)

        self.init_sail_res_menu()
        self.init_sail_com_menu()
        self.init_sail_map_menu()
        
        self.panel_sail.show()

    def init_sail_res_menu(self):
        self.mc = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 30), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="You", manager=self.manager,container= self.panel_sail_res)
        self.mc_des = pygame_gui.elements.UITextBox("Health: x \nhappienss: y\n",relative_rect=pygame.Rect((50, 70), (200, 100)),  manager=self.manager,container= self.panel_sail_res)

        self.ship = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 300), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Ship", manager=self.manager,container= self.panel_sail_res)
        self.ship_des = pygame_gui.elements.UITextBox("Damage: x\n ",relative_rect=pygame.Rect((50, 340), (200, 100)),  manager=self.manager,container= self.panel_sail_res)
        
        self.res = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 30), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Resources", manager=self.manager,container= self.panel_sail_res)
        self.res_des = pygame_gui.elements.UITextBox("Food: x\n Meds: \n Parts\n",relative_rect=pygame.Rect((350, 70), (200, 100)),  manager=self.manager,container= self.panel_sail_res)

        self.info = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((650, 30), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Information", manager=self.manager,container= self.panel_sail_res)
        self.info_des = pygame_gui.elements.UITextBox("you know that: x \n ",relative_rect=pygame.Rect((650, 70), (200, 100)),  manager=self.manager,container= self.panel_sail_res)

        self.item_dropdown = pygame_gui.elements.UIDropDownMenu(self.items, relative_rect=pygame.Rect((350, 350), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)),starting_option=self.items[0], manager=self.manager,container=self.panel_sail_res) 
        self.usage_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 400), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Use item", manager=self.manager,container= self.panel_sail_res)
    
    def init_sail_com_menu(self):
        
        info_view = pygame_gui.elements.UITextBox("Info:", relative_rect=pygame.Rect((500, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager,container=self.panel_sail_com)

        
        for i, char in enumerate(self.characters):
            label = pygame_gui.elements.UILabel(text = char+ " Ask about: ",relative_rect=pygame.Rect((60,50 + i * 100), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), manager=self.manager,container=self.panel_sail_com)
            question_dropdown = pygame_gui.elements.UIDropDownMenu(['lokalizacja','Dupa'], relative_rect=pygame.Rect((220, 50 + i * 100), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option='Dupa', manager=self.manager,container=self.panel_sail_com)
            question_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((380, 50 + i * 100), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Ask", manager=self.manager,container= self.panel_sail_com)


    def init_sail_map_menu(self):
         #wyspy
        self.past_isl1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 30), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island1", manager=self.manager,container= self.panel_sail_map)
        self.past_isl1_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((50, 70), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        self.past_isl2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 200), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island2", manager=self.manager,container= self.panel_sail_map)
        self.past_isl2_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((50, 240), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        self.past_isl3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 370), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island3", manager=self.manager,container= self.panel_sail_map)
        self.past_isl3_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((50, 410), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        self.isl1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((450, 30), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island1", manager=self.manager,container= self.panel_sail_map)
        self.isl1_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((450, 70), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        self.isl2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((450, 200), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island2", manager=self.manager,container= self.panel_sail_map)
        self.isl2_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((450, 240), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        self.isl3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((450, 370), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island3", manager=self.manager,container= self.panel_sail_map)
        self.isl3_des = pygame_gui.elements.UITextBox("x is here \nthere are y of resource",relative_rect=pygame.Rect((450, 410), (200, 100)),  manager=self.manager,container= self.panel_sail_map)

        #guziki przejscia do wysp
        self.isl1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 100), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island1", manager=self.manager,container= self.panel_sail_map)
        self.isl2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 270), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island2", manager=self.manager,container= self.panel_sail_map)
        self.isl3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 440), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Island3", manager=self.manager,container= self.panel_sail_map)
        

    def init_island_menu(self):
        self.panel_island = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)), manager=self.manager)

        #wydrukuj informacje o wyspach
        self.info_view = pygame_gui.elements.UITextBox("Info:", relative_rect=pygame.Rect((50, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager,container=self.panel_island)
        #self.info_view.set_text(self.sail_planner.print_islands())
        
        #guziki wyboru akcji
        self.next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Next", manager=self.manager,container=self.panel_island)
        self.escape_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 540), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Escape", manager=self.manager,container=self.panel_island)
        self.act_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 475), (MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)), text="Act", manager=self.manager,container=self.panel_island)
        
        
        #tekst wyswietlajacy co się dzieje
        self.text_view = pygame_gui.elements.UITextBox("Akcje:", relative_rect=pygame.Rect((550, 50 ), (LIST_VIEW_WIDTH, LIST_VIEW_HEIGHT)), manager=self.manager,container=self.panel_island)
        self.text_view.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
       
        #określenie akcji
        actions = ["ask_for_location","attack_for_location","ask_for_item","take_item","give_item","use_meds","rest", "attack", "spend_time_together"]
        self.action_dropdown = pygame_gui.elements.UIDropDownMenu(actions, relative_rect=pygame.Rect((50, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=actions[0], manager=self.manager,container=self.panel_island)
        
        self.character_dropdown = pygame_gui.elements.UIDropDownMenu(self.characters, relative_rect=pygame.Rect((250,475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=self.characters[0], manager=self.manager,container=self.panel_island)
        #items = ["Food","Gold","Fuel","Meds"]
        
        self.item_dropdown = pygame_gui.elements.UIDropDownMenu(self.items, relative_rect=pygame.Rect((450, 475), (OPTION_DROPDOWN_WIDTH, OPTION_DROPDOWN_HEIGHT)), starting_option=self.items[0], manager=self.manager,container=self.panel_island)


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


                    elif event.ui_element == self.res_button:
                        self.panel_sail_com.hide()
                        self.panel_sail_map.hide()
                        self.panel_sail_res.show()

                    elif event.ui_element == self.map_button:
                        self.panel_sail_com.hide()
                        self.panel_sail_map.show()
                        self.panel_sail_res.hide()
                    
                    elif event.ui_element == self.com_button:
                        self.panel_sail_com.show()
                        self.panel_sail_map.hide()
                        self.panel_sail_res.hide()
                    
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

                        self.panel_island.show()
                        self.panel_sail.hide()

                    

                        self.text_view.clear()
                        self.info_view.set_text(self.planner.print_state())
                        
                    elif event.ui_element == self.escape_button:
                        
                        self.sail_planner.update_world(self.planner.world_state)
                        #nowe wyspy
                        self.sail_planner.create_islands()
                        self.info_view.set_text(self.sail_planner.print_islands())

                        #update world state
                        
                        self.panel_island.hide()
                        self.panel_sail.show()

                        self.panel_sail_com.hide()
                        self.panel_sail_map.show()
                        self.panel_sail_res.hide()

                        

                if event.type == pygame.QUIT:
                    running = False
                self.manager.process_events(event)

            self.manager.update(time_delta)
            #self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()

        pygame.quit()

def main():
    game = GameGUI()
    game.main_loop()

if __name__ == "__main__":
    main()

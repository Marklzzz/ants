
import random
import string
import hashlib
import test
import pygame

pygame.init()
window = pygame.display.set_mode((500, 200))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

displayname_box = test.TextInputBox(50, 50, 400, font, 'Displayname')
email_box = test.TextInputBox(50,80,400,font, 'Email')
pwd_box = test.TextInputBox(50,110,400,font,'Password')
group = pygame.sprite.Group(displayname_box)
group.add(email_box)
group.add(pwd_box)

Result = {}
users = []
mails = []

for user in users:
    mails.append(user.mail)

run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for box in group:
                    Result[box.inactive_text]=box.text
                print(Result)
                register(Result['Email'],Result['Password'],Result['Displayname'],users)
                print(users)
                run = False
    group.update(event_list, Result)

    window.fill(0)
    group.draw(window)
    pygame.display.flip()


pygame.quit()
exit()
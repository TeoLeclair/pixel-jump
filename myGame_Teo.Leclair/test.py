# this prevents the player from jumping up through a platform
                elif self.player.vel.y <= 0:
                    if self.player.rect.top >= hits[0].rect.top - 5:    
                        self.player.vel.y = -self.player.vel.y
            ghits = pg.sprite.collide_rect(self.player, self.ground)
            if ghits:
                self.player.pos.y = self.ground.rect.top
                self.player.vel.y = 0


# this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = -10
                self.player.vel.y = -10
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom


if self.health == 0:
            self.pos = vec(WIDTH/2, HEIGHT/2)
            self.health = 5
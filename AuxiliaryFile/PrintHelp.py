"""
点:              print('point:',self.point.x,self.point.y)
线：             print('line:',self.line.start_point.x,self.line.start_point.y)
线方向：         print('dir:',self.line.direction.x,self.line.direction.y)
矩形：           print('rect:',self.rect.A.x, self.rect.A.y, self.rect.B.x, self.rect.B.y,\
                        self.rect.C.x, self.rect.C.y,self.rect.D.x, self.rect.D.y)

圆:
鼠标位置：
鼠标中键：
鼠标位置转成点：myPoint(event.pos().x(),event.pos().y())
图片路径：      './image/cv_team.jpg'
模块测试：     if __name__=='__main__':
弧度转角度：  (180/math.pi)*a
连接信号与槽(action)： self.delete_action.triggered.connect(self.delete_item)   #action
QStringList   ['a','b']

"""
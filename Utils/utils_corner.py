from PySide6.QtGui import QPainterPath, QRegion

# Function to apply rounded corners to QLabel
def applyRoundedCorners(label, radius_top_left, radius_bottom_left, radius_top_right, radius_bottom_right):
    rect = label.rect()  # Get the QLabel's rectangle
    path = QPainterPath()

    # Define the rounded rectangle with custom corner radii
    path.moveTo(rect.x() + radius_top_left, rect.y())
    path.arcTo(rect.x(), rect.y(), 2 * radius_top_left, 2 * radius_top_left, 90, 90)  # Top-left corner
    path.lineTo(rect.x(), rect.bottom() - radius_bottom_left)
    path.arcTo(rect.x(), rect.bottom() - 2 * radius_bottom_left, 2 * radius_bottom_left, 2 * radius_bottom_left, 180, 90)  # Bottom-left corner
    path.lineTo(rect.right() - radius_bottom_right, rect.bottom())
    path.arcTo(rect.right() - 2 * radius_bottom_right, rect.bottom() - 2 * radius_bottom_right, 2 * radius_bottom_right, 2 * radius_bottom_right, 270, 90)  # Bottom-right corner
    path.lineTo(rect.right(), rect.y() + radius_top_right)
    path.arcTo(rect.right() - 2 * radius_top_right, rect.y(), 2 * radius_top_right, 2 * radius_top_right, 0, 90)  # Top-right corner
    path.closeSubpath()

    # Apply mask to the QLabel
    mask = QRegion(path.toFillPolygon().toPolygon())
    label.setMask(mask)

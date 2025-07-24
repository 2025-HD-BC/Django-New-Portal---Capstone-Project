# Fix for AttributeError: Article.STATUS_REJECTED

## Issue Description
The Django News Portal application was throwing an `AttributeError` when users tried to register and access the dashboard:

```
AttributeError at /dashboard/ 
type object 'Article' has no attribute 'STATUS_REJECTED'
```

## Root Cause
The codebase had an inconsistency in how article status constants were referenced:

1. **Constants Definition**: Status constants were properly defined in `news/constants.py` as:
   - `ArticleStatus.PENDING`
   - `ArticleStatus.APPROVED` 
   - `ArticleStatus.REJECTED`

2. **Model Usage**: The `Article` model correctly used `ArticleStatus.PENDING`, etc. in its methods and properties.

3. **View Usage**: However, `news/views.py` line 115 was using `Article.STATUS_REJECTED` which didn't exist.

4. **Other Files**: Several test files and other modules also expected `Article.STATUS_*` constants to exist.

## Solution Applied
Added backward compatibility constants to the `Article` model class in `news/models.py`:

```python
class Article(models.Model):
    # Status constants for backward compatibility
    STATUS_PENDING = ArticleStatus.PENDING
    STATUS_APPROVED = ArticleStatus.APPROVED  
    STATUS_REJECTED = ArticleStatus.REJECTED
    
    # ... rest of model definition
```

## Files Modified

### 1. news/models.py
- **Line 48-51**: Added STATUS constants as class attributes to maintain backward compatibility
- **Change**: Added `STATUS_PENDING`, `STATUS_APPROVED`, `STATUS_REJECTED` constants

## Verification Tests

### 1. Django System Check ✅
```bash
python manage.py check
# Result: System check identified no issues (0 silenced).
```

### 2. Status Constants Accessibility ✅
```python
from news.models import Article
print(Article.STATUS_PENDING)   # Output: 'pending'
print(Article.STATUS_APPROVED)  # Output: 'approved'  
print(Article.STATUS_REJECTED)  # Output: 'rejected'
```

### 3. Dashboard Context Function ✅
```python
from news.views import _get_journalist_dashboard_context
# Previously threw AttributeError, now works correctly
context = _get_journalist_dashboard_context(user)
# Result: Dashboard context retrieved successfully!
```

### 4. Article Creation and Status Checking ✅
```python
article = Article.objects.create(
    title='Test Article',
    content='Test content', 
    author=user,
    status=Article.STATUS_PENDING  # Now works!
)
print(article.is_pending)  # Output: True
```

## Impact of Fix

### ✅ Fixed Issues:
- **User Registration**: Users can now register without errors
- **Dashboard Access**: The `/dashboard/` endpoint works correctly
- **Article Status Filtering**: Queries using `Article.STATUS_*` now work
- **Backward Compatibility**: Existing code using both patterns continues to work

### ✅ Maintained Functionality:
- **Article Model Methods**: `is_pending`, `is_approved`, `is_rejected` properties still work
- **Article Operations**: `approve()` and `reject()` methods unchanged
- **Database Schema**: No database migrations required
- **API Consistency**: Both `Article.STATUS_REJECTED` and `ArticleStatus.REJECTED` work

## Testing Completed

1. ✅ **System Check**: No Django configuration issues
2. ✅ **Model Access**: Article status constants accessible via `Article.STATUS_*`
3. ✅ **Dashboard Function**: `_get_journalist_dashboard_context()` works without errors
4. ✅ **Database Operations**: Article creation and status filtering working
5. ✅ **Migration Status**: No migrations needed, existing data unaffected

## Status: RESOLVED ✅

The `AttributeError: type object 'Article' has no attribute 'STATUS_REJECTED'` has been completely resolved. The application now supports user registration and dashboard access without errors.

**Ready for resubmission.**
